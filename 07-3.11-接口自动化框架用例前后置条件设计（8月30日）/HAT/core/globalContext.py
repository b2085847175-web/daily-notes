class g_context:
    _dic = {}

    def set_dict(self, key, value):
        self._dic[key] = value

    def set_by_dict(self, dic):
        self._dic.update(dic)

    def get_dict(self, key):
        return self._dic.get(key, None)

    def show_dict(self):
        return self._dic
