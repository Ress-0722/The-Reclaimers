import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = { 'up': False, 'down': False, 'right': False, 'left': False}
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    
    # Remove the rect() method entirely
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = { 'up': False, 'down': False, 'right': False, 'left': False}
       
        self.velocity[1] += 0.3
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        # Update rect position to match current pos
        self.pos[0] += frame_movement[0]
        self.rect.x = self.pos[0]  # Update rect after position change
        
        entity_rect = self.rect.copy()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                self.rect.x = self.pos[0]
        
        self.pos[1] += frame_movement[1]
        self.rect.y = self.pos[1]
        
        entity_rect = self.rect.copy()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 0
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
        
                self.pos[1] = entity_rect.y
                self.rect.y = self.pos[1]  # Update rect after position change
       
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf, offset=(0,0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
