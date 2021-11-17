import numpy as np

class allocation:
    def __init__(self) -> None:
        self.max_queue_two_one = 8
        self.max_queue_tree_zero = 10
        self.group_id_queue = []
        self.user_id_queue = []
        self.user_channel_queue = []
        self.already_assigned = []
        self.trios_created_counter = -1
        pass

    def set_trio(self, group_id, user_id, user_channel):
        self.group_id_queue.append(group_id)
        self.user_id_queue.append(user_id)
        self.user_channel_queue.append(user_channel)
        trio_finished, two_one_ready, three_zero_ready = self.is_trio_ready()

        if trio_finished and not (two_one_ready or three_zero_ready):
            trio_id, trio_member_list, trio_channel_list = self.create_trio()
        elif two_one_ready:
            trio_id, trio_member_list, trio_channel_list = self.create_trio_two_one()
        elif three_zero_ready:
            trio_id, trio_member_list, trio_channel_list = self.create_trio_three_zero()
        else:
            trio_id = []
            trio_member_list = []
            trio_channel_list = []

        self.already_assigned.extend(trio_member_list)

        print(group_id, user_id, user_channel)
        print(self.group_id_queue)

        return trio_finished, trio_id, trio_member_list, trio_channel_list 

    def is_trio_ready(self):
        num_unique_groups_in_queue = np.shape(np.unique(self.group_id_queue))[0]
        
        if num_unique_groups_in_queue >= 3:
            return True, False, False
        elif len(self.group_id_queue) >= self.max_queue_two_one and num_unique_groups_in_queue == 2:
            return True, True, False
        elif len(self.group_id_queue) >= self.max_queue_tree_zero and num_unique_groups_in_queue == 1:
            return True, False, True
        else:
            return False, False, False
    
    def create_trio(self):
        trio_member_list = []
        trio_channel_list = []

        for group_number in np.unique(self.group_id_queue):
            index = self.group_id_queue.index(group_number)
            self.group_id_queue.pop(index)
            trio_member_list.append(self.user_id_queue.pop(index))
            trio_channel_list.append(self.user_channel_queue.pop(index))
        
        self.trios_created_counter += 1

        return self.trios_created_counter, trio_member_list, trio_channel_list
    
    def create_trio_two_one(self):
        trio_member_list = []
        trio_channel_list = []  

        for group_number in np.unique(self.group_id_queue):
            index = self.group_id_queue.index(group_number)
            self.group_id_queue.pop(index)
            trio_member_list.append(self.user_id_queue.pop(index))
            trio_channel_list.append(self.user_channel_queue.pop(index))

        self.group_id_queue.pop(0)
        trio_member_list.append(self.user_id_queue.pop(0))
        trio_channel_list.append(self.user_channel_queue.pop(0))
    
        self.trios_created_counter += 1

        return self.trios_created_counter, trio_member_list, trio_channel_list

    def create_trio_three_zero(self):
        trio_member_list = []
        trio_channel_list = []

        for num in range(3):
            self.group_id_queue.pop(0)
            trio_member_list.append(self.user_id_queue.pop(0))
            trio_channel_list.append(self.user_channel_queue.pop(0))

        self.trios_created_counter += 1

        return self.trios_created_counter, trio_member_list, trio_channel_list
    
    def force_trio_creation(self):
        trios_id = []
        trios_member_list = []
        trios_channel_list = []

        while(len(self.group_id_queue)>0):
            if len(self.group_id_queue) == 4:
                id, member_list, channel_list = self.forma_primeira_de_duas_duplas()
                trios_id.append(id)
                trios_member_list.append(member_list)
                trios_channel_list.append(channel_list)
                
                id, member_list, channel_list =  self.forma_uma_dupla()

            elif len(self.group_id_queue) == 3:
                id, member_list, channel_list =  self.forma_um_trio()

            elif len(self.group_id_queue) == 2:
                id, member_list, channel_list =  self.forma_uma_dupla()

            elif len(self.group_id_queue) == 1:
                id, member_list, channel_list = self.forma_dupla_com_um_de_nos()

            else:
                id, member_list, channel_list = self.forma_um_trio()
            
            trios_id.append(id)
            trios_member_list.append(member_list)
            trios_channel_list.append(channel_list)
        
        return trios_id, trios_member_list, trios_channel_list

    def forma_primeira_de_duas_duplas(self):
        num_unique_groups_in_queue = np.shape(np.unique(self.group_id_queue))[0]
          
        if num_unique_groups_in_queue == 2:
            dupla1_member_list = []
            dupla1_channel_list = []

            for group_number in np.unique(self.group_id_queue):
                index = self.group_id_queue.index(group_number)
                self.group_id_queue.pop(index)
                dupla1_member_list.append(self.user_id_queue.pop(index))
                dupla1_channel_list.append(self.user_channel_queue.pop(index))
            
            self.trios_created_counter += 1 
        else:
            _, dupla1_member_list, dupla1_channel_list  = self.forma_uma_dupla()

        return self.trios_created_counter, dupla1_member_list, dupla1_channel_list

    def forma_uma_dupla(self):
        dupla_member_list = []
        dupla_channel_list = []
        self.group_id_queue.pop(0)
        self.group_id_queue.pop(0)
        dupla_member_list.append(self.user_id_queue.pop(0))
        dupla_channel_list.append(self.user_channel_queue.pop(0))
        dupla_member_list.append(self.user_id_queue.pop(0))
        dupla_channel_list.append(self.user_channel_queue.pop(0)) 

        self.trios_created_counter += 1 
        
        return self.trios_created_counter, dupla_member_list, dupla_channel_list

    def forma_dupla_com_um_de_nos(self):
        self.group_id_queue.pop(0)
        self.trios_created_counter += 1 
       
        return self.trios_created_counter, self.user_id_queue.pop(0), self.user_channel_queue.pop(0)

    def forma_um_trio(self):
        num_unique_groups_in_queue = np.shape(np.unique(self.group_id_queue))[0]
        if num_unique_groups_in_queue == 2:
            _, trio_member_list, trio_channel_list = self.create_trio_two_one()
        else:
           _, trio_member_list, trio_channel_list = self.create_trio_three_zero()

        self.trios_created_counter += 1 
        
        return self.trios_created_counter, trio_member_list, trio_channel_list

    def is_user_in_queue(self, user_id):
        return False
        #return (user_id in self.user_id_queue)
    
    def is_user_already_assigned(self, user_id):
        return False
        #return (user_id in self.already_assigned)
            
