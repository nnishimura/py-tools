#
# Pyton program for Project 3, 2013s1
#
# Author: Naoko Nishimura
#
# User name: nnishimura
#
# Student ID: 620011
#
# Date: 12/5/27
#
# Modified 12/5/27 to modify play
#


from collections import defaultdict

strength={'A':13,'K':12,'Q':11,'J':10,'0':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}

cards=[]
def sort_hand_tuples(cards):
    '''make a list of tuples and sort it by the length of each suit
    and the lists inside by strength'''
    '''[(suit,[card]),(suit,[card,card_stronger,...])]'''
    
    mydict=defaultdict(list)
    for card in cards:
        mydict[card[1]].append(card)#suitlist.append('KH'etc)
        '''map suit with cards that have the suit'''
    
    tuples=[]
    for suit,cards in mydict.iteritems():
        '''sort cards by actual strength'''
        tuples.append((suit,sorted(cards,key=lambda x:strength[x[0]])))
        '''tuples=[('H',[card,card_stronger])]'''
    
    tuples=sorted(tuples, key=lambda x:len(x[1]))
    '''sort the list of tuples by length of each suit'''
    
    return tuples

cards=[]
def sort_hand(cards):
    '''convert sort_hand_tuples(list) into a dict'''
    
    suit_dict={}
    for k,v in sort_hand_tuples(cards):
        suit_dict[k]=v
    
    return suit_dict

    
def pass_cards(hand):
    
    suit_dict=sort_hand(hand)
    suit_tuples=sort_hand_tuples(hand)
       
    output=[]
    '''store dengerous cards here first and do index slicing later'''
    
    swap_spade={'S':1,'H':0,'C':0,'D':0} 
    swap_heart={'S':0,'H':1,'C':0,'D':0} #will be used to sort tuples
    
    if 'S' in suit_dict.iterkeys() and len(suit_dict['S'])<=4:
        '''if spade is short in hand, pass QS & KS & AS but try keeping other cards'''
        
        new_hand=sorted(suit_tuples,key=lambda x:swap_spade[x[0]])
        '''put ('S',[card..]) in the end of list'''
        
        for card in hand:
            if card in ['QS','AS','KS']:
                output.append(card)
                
        global spade_sort
        spade_sort={'K':2,'A':1,'Q':0}
        '''put QS first in output'''
        output=sorted(output,key=lambda x:spade_sort[x[0]])
    
    
    elif len(suit_dict['H'])<=4:
        '''if heart is short in hand, pass strong heart cards but try to keep other cards'''
    
        suit_tuples=sorted(suit_tuples,key=lambda x:swap_heart[x[0]])
        '''put ('H',[card..]) in the end of list'''
    
        hearts=[]
    
        for card in hand:
            if card in ['AH','KH','QH']:
                hearts.append(card)
            
        hearts=sorted(hearts,key=lambda x:strength[x[0]],reverse=True)
        output.extend(hearts)
                    
    
    for mytuple in suit_tuples:
        output.extend(mytuple[1])

    
    return list(set(output))[:3]
            
def is_valid_play(played,hand,play,broken):
    
    suit_dict=sort_hand(hand)
    
    if play not in hand:
        return False
    
    else:
        if played==[]:#when i have the lead
            if (play[1]=='H' or play=='QS') and broken==False:
                if (suit_dict.keys()==['H']):
                    return True
                
                elif (suit_dict.keys()==['H','S'] or suit_dict.keys()==['S','H']) and suit_dict['S']==['QS']:
                    return True
            
                else:
                    return False
            else:
                return True
        
        elif played[0][1]==play[1]:
            '''lead suit==play'''
            return True
    
        elif played[0][1] not in suit_dict.keys():
            return True
        
        else:
            '''lead suit!=play, have other cards in hand'''
            return False
    
    
def get_valid_plays(played,hand,broken,is_valid=is_valid_play):
    '''if a card in hand is valid, add it to options'''
    
    options=[]
    for card in hand:
        if is_valid(played,hand,card,broken):
            options.append(card)
    
    return options

all_tricks=[]
stm=['QS','AH','KH','QH','JH','0H','9H','8H','7H','6H','5H','4H','3H','2H']

def test_stm(all_tricks):
    '''test if a player successed to do STM'''
    
    count=0
    for card in all_tricks:
        if card in stm:
            count+=1
    if count==len(stm):
        return True
    else:
        return False
        
def score_game(tricks_won):
    
    all_card=[]
    scores=[]
    score=0
    
    for player in tricks_won:
        
        for trick in player:
            '''put all cards which each player got together'''
            
            all_card.extend(trick)
        
            
        for card in all_card:
            
            if 'H' in card:
                score+=1
            elif 'QS'==card:
                score+=13
            elif '0D' == card:
                score-=10
                
        if test_stm(all_card):#STM
            score-=52 # -26+(-26)
        
        scores.append(score)
        '''calculate score for each player and add it to a list'''
        
        all_card=[]
        score=0
        
    score_win=[]
    for score in scores:
                
        if score==min(scores):
            score_win.append((score,True))
        else:
            score_win.append((score,False))

    return score_win

hand=[]
def voiding(hand):
       
    suit_tuples=sort_hand_tuples(hand)
    
    next_play=suit_tuples[0][1][0]
        
    
    if ('0D'==next_play) and (len(suit_tuples)>=2):
        '''try not to put 0D'''

        next_play=suit_tuples[1][1][0]

    elif next_play[1]=='H' and strength[next_play[0]]>=9:
        '''try not to put strong Heart'''
        
        if len(suit_tuples)>=2:
            
            next_play=suit_tuples[1][1][0]
        
    elif next_play[1]=='S' and strength[next_play[0]]>=11:
        '''try not to put spade stronger than QS'''
        
        if len(suit_tuples)>=2:
            
            next_play=suit_tuples[1][1][0]
                
    return next_play

def dump_dangerous_card(hand):
    
        
    output=[]
    for card in hand:
        
        if card in ['QS','KS','AS']:
            output.append(card)
    
    output=sorted(output,key=lambda x:spade_sort[x[0]])
    #spade_sort from pass_card()
    
    hearts=[]
    for card in hand:
        
        if card in ['AH','KH','QH']:
            hearts.append(card)
    output.extend(sorted(hearts,key=lambda x:strength[x[0]],reverse=True))

    if output==[]:
        return sort_hand_tuples(hand)[0][1][-1]
    
    else:
        return output[0]
    
           
played=[]
def avoid_points(hand,played):
        
    hand=sorted(hand,key=lambda x:strength[x[0]],reverse=True)#[strong--weak]
    
    max_strength=0
    for played_card in played:
        if played_card[1]==played[0][1] and strength[played_card[0]]>max_strength:
            '''if the current suit==other played card's suit'''
            max_strength=strength[played_card[0]]
    
    next_play=hand[0]
    for option in hand:
        '''pick the strongest card but weaker than the strongest card in played'''
        
        if strength[option[0]]<max_strength:
            next_play=option
            break
    
    return next_play

    
def play(tricks_won,played,hand,broken,is_valid=is_valid_play,
         valid_plays=get_valid_plays,score=score_game):
    
    all_tricks=[]
        
    for tricks in tricks_won:
        '''put all cards that each player got'''
        
        for trick in tricks:
            all_tricks.extend(trick)
    
    global all_tricks_won
    all_tricks_won=all_tricks
    
    
    options=valid_plays(played,hand,broken,is_valid=is_valid_play)
    '''put valid plays in a list'''

    if played==[]:
        
        return voiding(options)
    
    elif played[0][1] not in sort_hand(options).keys():
        
        return dump_dangerous_card(options)
    
    else:
        return avoid_points(options,played)
    
    
    ​
