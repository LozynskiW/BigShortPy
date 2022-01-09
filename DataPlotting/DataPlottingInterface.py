from abc import abstractmethod


class DataPlottingClassInterface:

    is_data_processor = True

    @abstractmethod
    def set_data(self, data):
        raise NotImplementedError

    @abstractmethod
    def plot_data(self):
        raise NotImplementedError