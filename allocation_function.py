import numpy as np

class allocation:
    def __init__(self) -> None:
        self.max_queue_two_one = 8
        self.max_queue_tree_zero = 12
        self.group_id_queue = []
        self.user_id_queue = []
        self.user_channel_queue = []
        self.already_assigned = []
        self.trios_created_counter = 0
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

        for index in range(3):
            self.group_id_queue.pop(index)
            trio_member_list.append(self.user_id_queue.pop(index))
            trio_channel_list.append(self.user_channel_queue.pop(index))

        self.trios_created_counter += 1

        return self.trios_created_counter, trio_member_list, trio_channel_list
    
    def is_user_in_queue(self, user_id):
        #return False
        return (user_id in self.user_id_queue)
    
    def is_user_already_assigned(self, user_id):
        return False
        #return (user_id in self.already_assigned)
            
