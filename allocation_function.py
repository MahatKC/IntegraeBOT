import numpy as np

class allocation:
    group_id_queue = []
    user_id_queue = []
    user_channel_queue = []

    def set_trio(self, group_id, user_id, user_channel):
        trio_finished = self.is_trio_ready(group_id)
        self.group_id_queue.append(group_id)
        self.user_id_queue.append(user_id)
        self.user_channel_queue.append(user_channel)

        if not trio_finished:
            trio_id = []
            trio_member_list = []
            trio_channel_list = []
        else:
            trio_id, trio_member_list, trio_channel_list = self.create_trio()

        return trio_finished, trio_id, trio_member_list, trio_channel_list 

    def is_trio_ready(self, group_id):
        if np.shape(np.unique(self.group_id_queue))[0] >= 3:
            return True
        else:
            return False
    
    def create_trio(self):
        trio_id = []
        trio_member_list = []
        trio_channel_list = []

        for group_number in np.unique(self.group_id_queue):
            index = self.group_id_queue.index(group_number)
            trio_id.append(self.group_id_queue.pop(index))
            trio_member_list.append(self.user_id_queue.pop(index))
            trio_channel_list.append(self.user_channel_queue.pop(index))

        return trio_id, trio_member_list, trio_channel_list