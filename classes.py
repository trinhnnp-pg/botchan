# Observer Pattern
class Subject():
    def __init__(self, call_back, value=0):
        self._observers = []
        self.value = value
        self.call_back = call_back
    
    def attach(self, observer):
        '''Append a new subsciber to the list if it doesn't exist in list'''
        for obs in self._observers:
            if obs.is_thesame(observer):
                return
        print('add user'+str(observer.observer_id))
        self._observers.append(observer)
    
    def detach(self, observer):
        '''Remove an subsciber from the list if it exists in list'''
        try:
            for obs in self._observers:
                if obs.is_thesame(observer):
                    self._observers.remove(obs)
                    print('remove user'+str(observer.observer_id))
                    return
        except ValueError:
            print("Observer is already not in the list of observers.")
    
    def change(self, value):
        '''Change value of subject and send notify'''
        self.value = value
        self.notify()

    def notify(self):
        '''Send notify to all observers'''
        new_value = self.value
        for observer in self._observers:
            observer.update(new_value, self.call_back)

class Observer():
    def __init__(self, observer_id):
        self.observer_id = observer_id
    
    def update(self, value, call_back):
        '''Alert method invoked when the notify() method in the subject is invoked.'''
        call_back(self, value)
    
    def is_thesame(self, observer):
        return self.observer_id == observer.observer_id
