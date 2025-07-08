import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def show_game_over(screen, font, score):
    """Show game over screen with score and menu options"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(game_over_text, game_over_rect)
    
    # Score text
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, score_rect)
    
    # Menu options
    new_game_text = font.render("Press R for New Game", True, (255, 255, 255))
    new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(new_game_text, new_game_rect)
    
    exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(exit_text, exit_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36) 
    
    game_over = False
    score = 0
    lives = PLAYER_LIFES

    def reset_game():
        nonlocal game_over, score, lives
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        asteroid_field = AsteroidField()
        game_over = False
        score = 0
        lives = PLAYER_LIFES
        return player, asteroid_field

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player, asteroid_field = reset_game()
    dt = 0
    respawn_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        player, asteroid_field = reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return
        
        if not game_over:
            if respawn_timer > 0:
                respawn_timer -= dt
            else:
                updatable.update(dt)

            for asteroid in asteroids:
                if player.alive() and asteroid.collides_with(player):
                    player.kill()
                    lives -= 1
                    if lives > 0:
                        respawn_timer = 0.5
                        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    else:
                        game_over = True
                    break
            
                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        score += 1
                        break

        screen.fill((0,0,0))
        
        if not game_over:
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))

            for item in drawable:
                item.draw(screen)
        else:
            # Draw final game state
            for item in drawable:
                item.draw(screen)
            # Show game over screen
            show_game_over(screen, font, score)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
if __name__ == "__main__":
    main()