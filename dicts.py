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


class MapRecursive(dict):
    # Proc_id, seq_record={stuff}
    def __init__(self, *args, **kwargs):
        super(MapRecursive, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    # print(k, type(k), v, type(v))
                    if type(v) is dict:
                        v = MapRecursive(v)
                    else:
                        pass
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                #print('kwargs')
                if isinstance(v, dict):
                    # print('\t', v, type(v))
                    v = MapRecursive(v)
                    #print('\t', v, type(v))
                    self[k] = v
                else:
                    # print('notadict')
                    #print(k, type(k), v, type(v))
                    self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(MapRecursive, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(MapRecursive, self).__delitem__(key)
        del self.__dict__[key]

    """
    def __add__(self, other):
        #assert isinstance(other, RecBlastContainer), " Item being added is not a RecBlastContainer!"
        for k, v in other.items():
            if k in self.keys():
                if isinstance(self[k], RecBlastContainer):
                    if isinstance(other[k], RecBlastContainer):
                        self[k] += other[k]
                    else:
                        pass
                elif not isinstance(self[k], list):
                    self[k] = [self[k]]

                if not isinstance(other[k], list):
                    other[k] = [other[k]]
                self[k].append(other[k])
            else:
                self[k] = v
        return self
    """


class RecBlastContainer(dict):
    def __init__(self, *args, **kwargs):
        super(RecBlastContainer, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    k.replace('.', '_')
                    if type(v) is dict:
                        v = RecBlastContainer(v)
                    else:
                        pass
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                k.replace('.', '_')
                if k == 'proc_id':
                    if isinstance(v, int):
                        v = 'x' + str(v)
                    self.proc_id = v
                elif k == 'seq_record':
                    self.seq_record = v
                if isinstance(v, dict):
                    v = RecBlastContainer(v)
                    self[k] = v
                else:
                    self[k] = v

    def __getattr__(self, attr):
        try:
            self[attr]
        except KeyError:
            raise
        except AssertionError:
            raise
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

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self

    def __add__(self, other):
        assert isinstance(other, RecBlastContainer), "Other is not a RecBlastContainer!"
        try:
            self.proc_id
        except KeyError:
            raise Exception('Attribute proc_id must be defined!!!')
        try:
            self.seq_record
        except KeyError:
            raise Exception('Attribute seq_record must be defined!!!')
        if self.proc_id == other.proc_id:
            return RecBlastContainer({'proc_id': self.proc_id, self.seq_record.name.replace('.', '_'): self,
                                      other.seq_record.name.replace('.', '_'): other})
        else:
            return RecBlastContainer({str(self.proc_id): self, str(other.proc_id): other},
                                     proc_id=[self.proc_id, other.proc_id])

    def __str__(self, indent=''):
        strobj = ''
        if isinstance(self, dict):
            for k, v in self.items():
                if indent:
                    strobj += ''.join([indent, '|---- Key "', str(k), '":', '\n'])
                else:
                    strobj += ''.join([indent, '| Key "', str(k), '":', '\n'])
                if isinstance(v, dict):
                    indent += '\t'
                    strobj += v.__str__(indent)
                else:
                    strobj += ''.join(['\t', indent, '|---', str(v).replace('\n', '\n\t' + indent + '|--- '), '\n'])
        return strobj
