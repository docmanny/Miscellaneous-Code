class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


class RecBlastContainer(dict):
    # Proc_id, seq_record={stuff}
    def __init__(self, *args, **kwargs):
        super(RecBlastContainer, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    print(k, type(k), v, type(v))
                    if type(v) is dict:
                        v = RecBlastContainer(v)
                    else:
                        pass
                    self[k] = v
            else:
                print(arg)

        if kwargs:
            for k, v in kwargs.items():
                print('kwargs')
                if isinstance(v, dict):
                    """print(v,'isdict')
                    for k, q in v.items():
                        print(k, type(k), q, type(q))
                        self[k] = q
                    """
                    print('\t', v, type(v))
                    v = RecBlastContainer(v)
                    print('\t', v, type(v))
                    self[k] = v
                else:
                    print('notadict')
                    print(k, type(k), v, type(v))
                    self[k] = v
                #                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(RecBlastContainer, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(RecBlastContainer, self).__delitem__(key)
        del self.__dict__[key]


class RecBlastContainerplus(dict):
    # Proc_id, seq_record={stuff}
    def __init__(self, *args, **kwargs):
        super(RecBlastContainerplus, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
                    # RecBlastContainerplus(**arg)

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    self[k] = RecBlastContainerplus(v)
                    # for a, b in v.items():
                else:
                    self[k] = v
                #                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(RecBlastContainerplus, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(RecBlastContainerplus, self).__delitem__(key)
        del self.__dict__[key]

    def __add__(self, other):
        assert isinstance(other, RecBlastContainerplus), " Item being added is not a RecBlastContainer!"
        for k, v in other.items():
            if k in self.keys():
                if isinstance(self[k], RecBlastContainerplus):
                    if isinstance(other[k], RecBlastContainerplus):
                        self[k] += other[k]
                    else:
                        pass
                elif not isinstance(self[k], list):
                    self[k] = [self[k]]

                if not isinstance(other[k], list):
                    other[k] = [other[k]]
                self[k] += other[k]
            else:
                self[k] = v
        return self
