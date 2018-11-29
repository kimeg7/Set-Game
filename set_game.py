import numpy as np
import random
import pygame
import sys
               
screen_width = 800;screen_height = 600
message_x_left = screen_width-260;message_y_top = 100
noset_x_left = 600;noset_x_right = 700;noset_y_top = 200;noset_y_down = 250;noset_width = 100;noset_height = 50
reset_x_left = 600;reset_x_right = 700;reset_y_top = 300;reset_y_down = 350;reset_width = 100;reset_height = 50
exit_x_left = 600;exit_x_right = 700;exit_y_top = 400;exit_y_down = 450;exit_width = 100;exit_height = 50

red = (255,0,0);orange = (255,128,0);yellow = (255,255,0);green = (0,255,0);blue = (0,128,255)
magenta = (0,255,255);white = (255,255,255);gray = (128,128,128);black = (0,0,0);brown = (102,51,0)

shapes = ['rectangle','triangle','circle']
shape_colors = [red, yellow, blue]
background_colors = [white, gray, brown]

offset = 150;width = 100;height = 100;x_pos = 100;y_pos = 100
positions = [[x_pos,y_pos],[x_pos+offset,y_pos],[x_pos+2*offset,y_pos],[x_pos,y_pos+offset],\
             [x_pos+offset,y_pos+offset],[x_pos+2*offset,y_pos+offset],[x_pos,y_pos+2*offset],\
             [x_pos+offset,y_pos+2*offset],[x_pos+2*offset,y_pos+2*offset]]

class Card():
    def __init__(self, image, shape, color, background_color, pos, screen):
        self.screen = screen
        self.image = image
        self.shape = shape
        self.color = color
        self.background_color = background_color
        self.x = pos[0]
        self.y = pos[1]
        
    def draw(self):
        self.screen.blit(self.image, [self.x, self.y]) 
        
    def clear_selection(self):
        pygame.draw.rect(self.screen, black, (self.x-10,self.y-10,width+20,height+20))
        
def buttons(screen, noset, reset, exit):
    pygame.draw.rect(screen, white, (reset_x_left-3,reset_y_top-3,reset_width+6,reset_height+6))
    pygame.draw.rect(screen, green, (reset_x_left,reset_y_top,reset_width,reset_height))

    pygame.draw.rect(screen, white, (exit_x_left-3,exit_y_top-3,exit_width+6,exit_height+6))
    pygame.draw.rect(screen, red, (exit_x_left,exit_y_top,exit_width,exit_height))

    pygame.draw.rect(screen, white, (noset_x_left-3,noset_y_top-3,noset_width+6,noset_height+6))
    pygame.draw.rect(screen, yellow, (noset_x_left,noset_y_top,noset_width,noset_height))

    screen.blit(noset,(noset_x_left+15,noset_y_top+10))
    screen.blit(reset,(reset_x_left+15,reset_y_top+10))
    screen.blit(exit,(exit_x_left+25,exit_y_top+10))
    return

def all_combinations(shapes, shape_colors, background_colors):
    combinations = []
    for i in shapes:
        for j in shape_colors:
            for k in background_colors:
                combinations.append([i,j,k])
    return combinations

def load_images(combinations):
    images = []
    for i in range(len(combinations)):
        
        picture = pygame.image.load('images\\image_'+str(i+1)+'.png')
        picture = pygame.transform.scale(picture, (width,height))
        images.append(picture)
    return images

def display_cards(cards):
    for card in cards:
        card.clear_selection()
        card.draw()
    return
        
def reset_board(images,combinations,screen):
    cards = []
    clear_solutions(screen)
    random_choices = random.sample(range(0, len(combinations)), 9)

    for index in np.arange(len(random_choices)):
        card = Card(images[random_choices[index]],combinations[random_choices[index]][0], \
                    combinations[random_choices[index]][1],combinations[random_choices[index]][2],\
                    positions[index],screen)
        cards.append(card)  
        
    solutions = solve(cards)
    display_cards(cards)
    return cards, solutions

def solve(cards):
    solutions = []
    for i, group1 in enumerate(cards):
        for j, group2 in enumerate(cards):
            for k, group3 in enumerate(cards):
                score1 = 0; score2 = 0; penalty = 0
                if len(set([i,j,k]))==3 and i<j and j<k and i<k:
                    if len(set([group1.shape,group2.shape,group3.shape]))==1:   score1 += 1
                    elif len(set([group1.shape,group2.shape,group3.shape]))==2: penalty += 1
                    elif len(set([group1.shape,group2.shape,group3.shape]))==3: score2 += 1
                        
                    if len(set([group1.color,group2.color,group3.color]))==1:   score1 += 1
                    elif len(set([group1.color,group2.color,group3.color]))==2: penalty += 1
                    elif len(set([group1.color,group2.color,group3.color]))==3: score2 += 1
                        
                    if len(set([group1.background_color,group2.background_color,group3.background_color]))==1:   score1 += 1
                    elif len(set([group1.background_color,group2.background_color,group3.background_color]))==2: penalty += 1
                    elif len(set([group1.background_color,group2.background_color,group3.background_color]))==3: score2 += 1
                        
                if (score1 > 0 and penalty == 0) or score2 == 3: solutions.append([i,j,k])
    return solutions
                
def choose(mx,my,cards,screen):
    for index, card in enumerate(cards):
        if pygame.Rect((card.x,card.y,width,height)).collidepoint((mx,my)):
            highlight_choice(card,screen)
            return index
    return -1

def highlight_choice(card, screen):
    pygame.draw.rect(screen, green, (card.x-10,card.y-10,width+20,height+20))
    card.draw()    
    return

def remove_highlighted(cards,correct_cards, screen):
    
    for card in correct_cards:
        pygame.draw.rect(screen, black, (cards[card].x-10,cards[card].y-10,width+20,height+20))
        cards[card].draw()
    return

def remove_double_clicked(cards,card,screen):
    pygame.draw.rect(screen, black, (cards[card].x-10,cards[card].y-10,width+20,height+20))
    cards[card].draw()
    return
  
def check(chosen_cards, solutions):
    for solution in solutions:
        if set(chosen_cards) == set(solution):
            return chosen_cards
    return -1

def check_duplicate(correct_cards,correct_cards_box):
    for group in correct_cards_box:
        if set(correct_cards)==set(group):
            return True
    return False

def display_match(correct_cards, cards, screen, answer_set_count):
    offset = 0
    for card in correct_cards:
        image = pygame.transform.scale(cards[card].image, (30,30))
        screen.blit(image, [30 + offset + 120*(answer_set_count-1), 30])
        offset += 35
    return

def display_message(message, screen):
    pygame.draw.rect(screen, black, (message_x_left, message_y_top,250,40))
    screen.blit(message,(message_x_left, message_y_top))
    return

def clear_solutions(screen):
    pygame.draw.rect(screen, black, (0,0,screen_width,80))
    pygame.draw.rect(screen, black, (message_x_left, message_y_top,250,80))
    return

def no_set_decision(mx, my, images, combinations, screen, answer_set_count, solutions, find_more_sets):
    if pygame.Rect((noset_x_left,noset_y_top,noset_width,noset_height)).collidepoint((mx,my)):
        if answer_set_count >= len(solutions):
            print('      Complete')
            cards, solutions = reset_board(images,combinations,screen)
            return cards, solutions
        display_message(find_more_sets, screen)
    return -1, -1
        
def initialize_game_settings():
    pygame.init()
    pygame.font.init() 
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Set Game')
    font = pygame.font.SysFont('Comic Sans MS', 20)
    noset = font.render('No Set', False, (0, 0, 0))
    reset = font.render('RESET', False, (0, 0, 0))
    exit = font.render('EXIT', False, (0, 0, 0)) 
    correct = font.render('Correct Set!', False, (255, 255, 255)) 
    incorrect = font.render('Incorrect Set!', False, (255, 0, 0)) 
    duplicate = font.render('This Set Is Already Found!', False, (255, 0, 0)) 
    find_more_sets = font.render('Find More Sets!', False, (255, 0, 0)) 
    no_set = font.render('Good! All Sets Found!', False, (255, 255, 255)) 
    
    
    clock = pygame.time.Clock()
    
    return screen, noset, reset, exit, clock, correct, incorrect, duplicate, find_more_sets, no_set
    
def main():
    screen, noset, reset, exit, clock, correct, incorrect, duplicate, find_more_sets, no_set = initialize_game_settings()
    combinations = all_combinations(shapes, shape_colors, background_colors)
    images = load_images(combinations)
    buttons(screen, noset, reset, exit)
    cards = []; solutions = []; chosen_cards = []; correct_cards_box = []; answer_set_count = 0
    
    cards, solutions = reset_board(images,combinations,screen)       
        
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                break
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if pygame.Rect((exit_x_left,exit_y_top,exit_width,exit_height)).collidepoint((mx,my)): 
                    crashed = True
                    break
                    
                if pygame.Rect((reset_x_left,reset_y_top,reset_width,reset_height)).collidepoint((mx,my)): 
                    cards, solutions = reset_board(images,combinations,screen)       
                    chosen_cards = []; correct_cards_box = []; answer_set_count = 0
                
                if len(cards)>0:
                    answer_card = choose(mx,my,cards,screen)
                    
                    if not answer_card == -1:
                        if answer_card not in chosen_cards: chosen_cards.append(answer_card)
                        else:
                            for index, element in enumerate(chosen_cards):
                                if element == answer_card:
                                    chosen_cards.pop(index)
                                    remove_double_clicked(cards,element,screen)
                                    break
                                                
                    
                    if len(chosen_cards) == 3:
                        correct_cards = check(chosen_cards, solutions)
                        
                        if correct_cards == -1:
                            remove_highlighted(cards,chosen_cards,screen)
                            display_message(incorrect, screen)
                            print('     incorrect set!')
                            chosen_cards = []
                            
                        else:
                            
                            is_duplicate = check_duplicate(correct_cards,correct_cards_box)
                            
                            if not is_duplicate:
                                display_message(correct, screen)
                                print('     Match ',chosen_cards)                                
                                
                                correct_cards_box.append(correct_cards)
                                remove_highlighted(cards,correct_cards,screen)
                                answer_set_count += 1

                                if answer_set_count <= len(solutions):
                                    display_match(correct_cards, cards, screen, answer_set_count)
                                chosen_cards = []
                            else:
                                display_message(duplicate, screen)
                                print('     duplicate set!')    
                                
                                remove_highlighted(cards,correct_cards,screen)
                                chosen_cards = []
                                
                    new_cards, new_solutions = no_set_decision(mx, my, images, combinations, screen, answer_set_count, solutions, find_more_sets)
                    
                    if not new_cards == -1:
                        cards = new_cards
                        solutions = new_solutions
                        display_message(no_set, screen)
                        remove_highlighted(cards,chosen_cards,screen)
                        answer_set_count = 0; correct_cards_box = []

            pygame.display.update()
            clock.tick(60)

    pygame.quit()
    quit()       

if __name__=="__main__":
    main()
