class g_context:
    """全局变量容器，_dic 是类变量，用于多处共享数据"""

    _dic = {}

    def set_dict(self, key, value):
        self._dic[key] = value

    def set_by_dict(self, dic):
        self._dic.update(dic)

    def get_dict(self, key):
        return self._dic.get(key, None)

    def show_dict(self):
        return self._dic
