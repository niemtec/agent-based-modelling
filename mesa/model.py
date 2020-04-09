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