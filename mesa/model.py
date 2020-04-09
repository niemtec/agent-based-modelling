from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
class SchellingAgent(Agent):
   # Initialisation
   def __init__(self, pos, model, agent_type):
      super().__init__(pos, model)
      self.pos = pos
      self.type = agent_type

   # Step function
   def step(self):
      similar = 0
      # Calculate number of similar neighbours
      for neighbour in self.model.grid.neighbour_iter(self.pos):
         if neighbour.type == self.type:
            similar += 1

      # Move to a random empty location if unhappy
      if similar < self.model.homphily:
         self.model.grid.move_to_empty(self)
      else:
         self.model.happy += 1

class Schelling(Model):
   def __init__(height, width, density, minority_pc, homophily):
      # Width: Horizontal axis
      # Height: Vertical axis
      # Density: Population density (0-1)
      # Fraction Minority: Ratio between red/blue (blue being minority)
      # Homophily: Number of similar neighbours required for agents to be happy (0-8)
      self.height = height
      self.width = width
      self.density = density
      self.minority_pc = minority_pc
      self.homophily = homophily

      # Grid setup
      self.grid = SingleGrid(width, height, torus=True)
      
      # Scheduler setup
      self.schedule = RandomActivation(self)

      # Data collection setup
      self.happy = 0
      self.datacollector = DataCollector({"happy": "happy"}, {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
      
      # Agents setup
      for cell in self.grid.coord_iter():
         x = cell[1]
         y = cell[2]
         if self.random.random() < self.density:
            if self.random.random() < self.minority_pc:
               agent_type = 1
            else:
               agent_type = 0
         
         agent = SchellingAgent((x, y), self, agent_type)
         self.grid.position_agent(agent, (x, y))
         self.schedule.add(agent)

         self.running = True
         self.datacollector.collect(self)

   def step(self):
      self.happy = 0  # Reset the counter of happy agents
      self.schedule.step()
      # Collect data
      self.datacollector.collect(self)
      # Stop the model if all agents are happy
      if self.happy == self.schedule.get_agent_count():
         self.running = False
