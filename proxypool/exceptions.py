class EmptyException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


if __name__ == '__main__':
    try:
        raise EmptyException('空的')
    except EmptyException as e:
        print(e.error_info)
