from flight import Flight

class MinHeap:
    def __init__(self):
        self.data = []
    
    def push(self, item):
        self.data.append(item)
        self._shift_up(len(self.data) - 1)
    
    def pop(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        min_item = self.data[0]
        self.data[0] = self.data.pop()
        self._shift_down(0)
        return min_item
    
    def _shift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.data[index][0] < self.data[parent][0]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            self._shift_up(parent)
    
    def _shift_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.data) and self.data[left][0] < self.data[smallest][0]:
            smallest = left
        if right < len(self.data) and self.data[right][0] < self.data[smallest][0]:
            smallest = right
        if smallest != index:
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            self._shift_down(smallest)
    
    def is_empty(self):
        return len(self.data) == 0
class Planner:
    def __init__(self, flights):       
       max_city=-1
       for flight in flights:
           v=max((flight.start_city, flight.end_city))
           if v>max_city:
               max_city=v

       self.adjacency_list = [[] for _ in range(max_city + 1)]
       
       for flight in flights:
           self.adjacency_list[flight.start_city].append(flight)
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
       
       max_city = len(self.adjacency_list)
       num_flights = [float('inf')] * max_city 
       arrival_times = [float('inf')] * max_city  
       previous_flights = [None] * max_city  
       
       
       num_flights[start_city] = 0
       arrival_times[start_city] = t1
       
       
       queue = [(start_city, t1)]
       queue_start = 0  
       
      
       while queue_start < len(queue):
           current_city, current_time = queue[queue_start]
           queue_start += 1
           if current_time>t1:
               current_time += 20
           
           for flight in self.adjacency_list[current_city]:
               next_city = flight.end_city
               
               
               if flight.departure_time >= max(current_time, t1) and flight.arrival_time <= t2:
                   new_num_flights = num_flights[current_city] + 1
                   
                   
                   if (new_num_flights < num_flights[next_city] or 
                       (new_num_flights == num_flights[next_city] and 
                        flight.arrival_time < arrival_times[next_city])):
                       
                       num_flights[next_city] = new_num_flights
                       arrival_times[next_city] = flight.arrival_time
                       previous_flights[next_city] = flight
                       queue.append((next_city, flight.arrival_time))
       
       
       route = []
       current_city = end_city
       
       
       if num_flights[end_city] != float('inf'):
           while current_city != start_city:
               flight = previous_flights[current_city]
               if flight:
                   route.append(flight)
                   current_city = flight.start_city
               else:
                   break
           route.reverse()
           
       return route

    def cheapest_route(self, start_city, end_city, t1, t2):
        
        pq = MinHeap()
        pq.push((0, start_city, [], t1))
        min_cost = float('inf')
        best_route = None
        
        
        while not pq.is_empty():
            
            current_cost, current_city, route, current_time = pq.pop()
            
            
            
            
            if current_cost >= min_cost:
                continue
            
            
            if current_city == end_city and t1 <= current_time <= t2:
                
                
                if current_cost < min_cost:
                    
                    min_cost = current_cost
                    best_route = route[:]
                continue
            if current_time>t1:
                current_time+=20
            
            
            for flight in self.adjacency_list[current_city]:
                
                if flight.departure_time >= current_time and flight.departure_time >= t1 and flight.arrival_time <= t2:
                    
                    pq.push((current_cost + flight.fare, flight.end_city, route + [flight], flight.arrival_time))
                    
        
        
        return best_route if best_route is not None else []


        
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
       max_city = len(self.adjacency_list)
       num_flights = [float('inf')] * max_city 
       least_cost = [float('inf')] * max_city  
       previous_flights = [None] * max_city 
       routes=[[]]*max_city
       num_flights[start_city] = 0
       least_cost[start_city] = 0
       
       pq=MinHeap()
       pq.push((0,0,start_city,t1,[]))

       
       while not pq.is_empty():
           flight_count,total_cost,current_city, current_time,route=pq.pop()
           if current_time>t1:
               current_time += 20
           for flight in self.adjacency_list[current_city]:
               next_city = flight.end_city
               
               if flight.departure_time >= max(current_time, t1) and flight.arrival_time <= t2:
                   new_num_flights = num_flights[current_city] + 1
                   new_fare=total_cost + flight.fare
                   if (new_num_flights < num_flights[next_city] or 
                       (new_num_flights == num_flights[next_city] and 
                        new_fare < least_cost[next_city])):
                       
                       
                       routes[next_city]=route+[flight]
                       num_flights[next_city] = new_num_flights
                       least_cost[next_city] = new_fare
                       previous_flights[next_city] = flight
                       pq.push((new_num_flights, new_fare, next_city, flight.arrival_time,routes[next_city]))
       return routes[end_city]
       

        
            
        
        
        
     
            

