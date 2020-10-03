
class SwitchStats:
    def __init__(self, id):
        self.id = id
        self.stats = None

    def get_id(self):
        return self.id

    def get_stats(self):
        return self.stats

    def get_total_packet_count(self):
        return NotImplementedError

    def get_packet_count_from_src(self):
        return NotImplementedError

    def get_packet_count_from_dst(self):
        return NotImplementedError

    def get_packet_count_from_src_dst(self):
        return NotImplementedError