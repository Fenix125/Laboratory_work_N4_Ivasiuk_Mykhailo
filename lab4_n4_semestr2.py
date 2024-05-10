"""
Laboratory work N4, Ivasiuk Mykhailo
24 hours, 6 states, 6 random impacts on choices
"""
import time
import random

def prime(fn):
    """
    Using for correct yield functionality
    """
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

def slow_print(text, delay=0.1):
    """
    Slow prints text
    """
    for char in text[:-1]:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(text[-1], flush=True)
class Person:
    """
    Class person, needed to track 
    coefficient of person's well spent day
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.coeff = 0
class Day:
    """
    Day:
        - starts form slepping:
            1. Weekday:
                - wake up at 7 or 9
                - eating state: can give additional 
                    points if gained favourite dish
                - class time
                - social break: happens randomly
                - self study session: can earn coeff 
                    by doing homework, bigger chance 
                    if had breakfast
                - party: low chance, great coeff, lasts all day
            2. Weekend:
                choses randomly:
                    - gym: more coeff(favourite sport)
                    - running
                - eating
                - study session
                - eating
                choses randomly:
                    - social break 
                    - study session 
    """
    def __init__(self, pers: 'Person') -> None:
        self.sleep_state = self._sleep()
        self.study_state = self._study()
        self.class_time = self._class_time()
        self.eating_state = self._eating()
        self.social_break = self._social_break()
        self.current_state = self.sleep_state
        self.person = pers
        self._eaten_food = [False, False, False]
        self._late = False
        self._weekday = random.randint(1, 7) < 6

    def send(self, hour):
        """
        Send hour to yield func - "state"
        """
        try:
            self.current_state.send(hour)
        except StopIteration:
            pass
    @prime
    def _party(self):
        """
        Party state, chance: 4/100 
        """
        while True:
            hour = yield
            slow_print('PARTYING!!!!!' f'|hour= {hour}', 0.01)
            if hour == 24:
                slow_print('i ThiK, iT\'s timE tO Go to slEeP ((')
                return
            
    @prime
    def _sleep(self):
        """
        Sleep state, person either:
            - wakes up at 7, goes for a breakfast
            - wakes up at 9, runs to class
        """
        while True:
            hour = yield
            time.sleep(0.5)
            slow_print('zZzZzz.z..z.' f'|hour= {hour}')
            if self._weekday: #if weekday
                if random.randint(1, 100) <= 4: #party chance
                    slow_print('YOU KNOW WHAT? IT\'S TIME FOR A PARTY!!!' f'|hour= {hour}')
                    self.person.coeff += 3
                    self.current_state = self._party()
                    break
                if hour == 7 and random.randint(1, 100) < 80: #woke up in time
                    slow_print('Waking up' f'|hour= {hour}')
                    slow_print('.....', 0.5)
                    slow_print('\nWhat a beautiful day!' f'|hour= {hour}')
                    time.sleep(1)
                    slow_print('Its time for a breakfast' f'|hour= {hour}')
                    time.sleep(0.5)
                    self.person.coeff += 1
                    self.current_state = self.eating_state
                elif hour == 9: #oversleep
                    slow_print('.....', 0.5)
                    slow_print('\nOh no....i am late for my classes' f'|hour= {hour}')
                    self.current_state = self.class_time
                    self._late = True
                    time.sleep(1)
            else: #if weekend
                if hour == 4: #wakes up
                    slow_print('It\'s time to wake up, and do some work. :)))' f'|hour= {hour}')
                    slow_print('I think i will go....')
                    if random.randint(1, 10) <= 5: #gym
                        self.person.coeff += 2
                        slow_print('TO THE GYM!!')
                        self.current_state = self.go_gym()
                    else: #running
                        self.person.coeff += 1
                        slow_print('RUNNING')
                        self.current_state = self.go_running()
    @prime
    def go_gym(self):
        """
        Gym state
        """
        while True:
            hour = yield
            slow_print('training....' f'|hour= {hour}')
            if random.randint(1, 10) <= 2:
                slow_print('Yeah, made new personal record!!')
                self.person.coeff += 1
            if hour == 7:
                slow_print('What a great workout, it\'s time to have a breafast')
                self.current_state = self.eating_state

    @prime
    def go_running(self):
        """
        Running state
        """
        while True:
            hour = yield
            slow_print('running....' f'|hour= {hour}')
            if random.randint(1, 10) <= 2:
                slow_print('Woah, ran a great distance!')
                self.person.coeff += 1
            if hour == 7:
                slow_print('What a great marathon, it\'s time to have a breakfast')
                self.current_state = self.eating_state


    @prime
    def _study(self):
        """
        Study state, has chance(that depends on eaten food, 
        or (weekday / weekend)) to give extra coeff to person.
        """
        def extra_points_for_task(chance: int):
            """
            Gives extra points to person
            """
            if random.randint(1, 10) <= chance:
                slow_print('Yeah, made task for extra points')
                self.person.coeff += 1
        while True:
            hour = yield
            slow_print('Studying......' f'|hour= {hour}')
            if self._weekday: #weekday
                if hour == 19: #late study session
                    slow_print('i think it\'s time to have dinner' f'|hour= {hour}')
                    self.current_state = self.eating_state
                else: #extra points task
                    extra_points_for_task(5) if self._eaten_food[0] else extra_points_for_task(3)
            else: # weekend
                if hour == 14: #lunch
                    slow_print('woah, i have studied a lot, time to have a lunch')
                    self.current_state = self.eating_state
                elif hour == 19: #dinner
                    slow_print('it was nice day, i made a lot of work this day, i need to have a dinner')
                    self.current_state = self.eating_state
                else: #extra points
                    extra_points_for_task(6)

    @prime
    def _class_time(self):
        """
        Class time, randomly can get additional coeff
        """
        while True:
            hour = yield
            if 9 <= hour <= 14:
                if hour == 9:
                    slow_print('\nCame in time!' f'|hour= {hour}')
                elif self._late:
                    slow_print('.....', 0.5)
                    slow_print('I am so sorry for being late for class :(' f'|hour= {hour}')
                    self._late = False
                time.sleep(1)
                slow_print('Studying.....' f'|hour= {hour}')
                if self._eaten_food[0] is True:
                    if random.randint(1, 10) <= 4:
                        slow_print('Yeah, gained point for great questions')
                        self.person.coeff += 1
                else:
                    if random.randint(1, 10) <= 2:
                        slow_print('Yeah, gained point for great questions')
                        self.person.coeff += 1
                if hour == 14:
                    slow_print('.....', 0.5)
                    if self._eaten_food[0] is True:
                        slow_print('I think it\'s time to have a lunch')
                    else:
                        slow_print('I think it\'s time to have a lunch, i haven\'t eaten since morning :(')
                    self.current_state = self.eating_state

    @prime
    def _eating(self):
        """
        Eating state, has chance of giving extra coeff to person - if favourite food
        """
        def favourite_food():
            if random.randint(1, 10) < 5:
                slow_print('Wow, my favourite dish')
                self.person.coeff += 1
        while True:
            hour = yield
            if hour == 8: #breakfast
                favourite_food() #favourite food
                slow_print('Eating...' f'|hour= {hour}')
                time.sleep(1)
                slow_print(f'\nMmmm, what a nice breakfast, {"its time to attend classes" if self._weekday else "now i need to study"}|hour= {hour}')
                time.sleep(1)
                self._eaten_food[0] = True
                self.current_state = self.class_time if self._weekday else self.study_state
            elif hour == 15:
                favourite_food() #favourite food
                slow_print('Eating...' f'|hour= {hour}')
                time.sleep(1)
                slow_print('Mmmm, what a delicious lunch' f'|hour= {hour}')
                time.sleep(1)
                self._eaten_food[1] = True
                #chance of going chill after lunch depends on day
                if random.randint(1, 10) < 5 if self._weekday else random.randint(1, 10) < 7:
                    slow_print('Hmmmm, i think i will go chill with my friends for a few hours' f'|hour= {hour}')
                    self.person.coeff += 1
                    self.current_state = self.social_break
                else:
                    slow_print('Now i will go to study, need to do a lot of work, i think i will start with laboratory work on discrete mathematics' f'|hour= {hour}')
                    self.current_state = self.study_state
            elif hour == 20:
                favourite_food() #favourite food
                slow_print('Eating...' f'|hour= {hour}')
                time.sleep(1)
                slow_print('Mmmmm, what a nice dinner' f'|hour= {hour}')
                self._eaten_food[2] = True
                self.current_state = self.end_of_the_day()
    @prime
    def end_of_the_day(self):
        """
        End of the day, just returns
        """
        while True:
            hour = yield
            slow_print('i think it\'s time to go to sleep(' f'|hour= {hour}')
            return


    @prime
    def _social_break(self, once = 0):
        """
        Social break state
        """
        while True:
            hour = yield
            slow_print('Yeah, i like spending time with my friends') if once == 0 else ''
            once += 1
            slow_print('.....')
            slow_print('chilling...' f'|hour= {hour}')
            if hour == 16 and self._weekday:
                slow_print('I think it\'s time to study...')
                self.current_state = self.study_state
            elif hour == 19:
                slow_print('what a great day, now i need to have a dinner!')
                self.current_state = self.eating_state

def day(pers):
    """
    Starts day
    """
    if not isinstance(pers, Person):
        raise TypeError('Please provide an instance of class Person')
    day_of_person = Day(pers)
    for hour in range(1, 25):
        day_of_person.send(hour)
    time.sleep(2)
    slow_print('END OF THE DAY', 0.25)
    return f'Coefficient of well spent day of person: {person.name} - {person.coeff}'


#Create a person and call "day" function
person = Person('Mykhailo')
slow_print(day(person))

