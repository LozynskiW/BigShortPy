# Basic app structure
    StockData - queries data source and downloads data, stores data, 
    maps data between pandas, dicts and lists

    DataProcessing - processes given StockData and outputs analysis outcome
    which form is based on what outcome shows (may be list, dict, panda, any)
    
    Indicators - combination of StockDataHolder and selected DataProcessing 
    Class that provides easier way of getting financial analysis just by 
    providing StockData by user, as DataProcessing Class - 
    data_processor is already hard coded into Indicator. Also allows for
    further data processing based on information indicator must provide

    Signal - analyses outcome of indicator (DataProcessing Class), and based
    on current date or price of instruments outputs most probable strategy 
    direction in form of:
    
    {
    "overpriced": False,
    "underpriced": False,
    "undetermined": True,
    "strength": "strong"
    }

    Strategy - analyses given signals and makes a decision about trading
    oppurtunites

    TradingMemory - serves as memory for recent and historic decisions that
    allows for income calculation and closing positions

    StrategyTester - allows for strategy testing based on provided timespan
    
    
## StockData   
### Members:    

-> **QueryAssistanceModule:** Forms queries needed for DataDownload Classes to download data  
-> **DataDownloadModule:** Downloads data from selected source (online or offline) based on provided query  
-> **StockData:** by DataDownloadModule it downloads and contains financial data, 
    providing tools to change form of data to list or dicts

## DataProcessing
### Class Structure
    is_data_processor = True

    @abstractmethod
    def set_stock_data(self, stock_data):
        raise NotImplementedError

    @abstractmethod
    def get_data_from_data_source(self):
        raise NotImplementedError

    @abstractmethod
    def convert_data(self):
        raise NotImplementedError

    @abstractmethod
    def get_analysis_outcome(self):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError
### Usage

Based on provided StockDataHolder processes data to form best suiting output of processing. 
Data then can be used for further processing (in IndicatorsCalculation) or analysis by plotting

## IndicatorsCalculation
### Class Structure
    is_indicator = True
    __analysis_engine = None

    @abstractmethod
    def set_stock_data(self, stock_data):

        if self.__analysis_engine is None:
            raise AttributeError
        else:
            self.__init_analysis_engine(stock_data=stock_data)

        self.__set_required_analysis_outcome()

        raise NotImplementedError

    @abstractmethod
    def __set_required_analysis_outcome(self):
        raise NotImplementedError

    @abstractmethod
    def __init_analysis_engine(self, stock_data):
        raise NotImplementedError

    @abstractmethod
    def calculate_indicator(self):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError

### Usage
Indicator is a combination of StockDataHolder and selected DataProcessing Class that provides easier
way of getting financial analysis just by providing StockData by user, as DataProcessing Class - data_processor
is already set.

## Signal
### Class Structure
**Based on PriceLevel**

    is_signalInterpreterClass = True
    signal_per_price = []

    @abstractmethod
    def set_data(self, data):
        """of type DataProcessing or Indicator"""
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_price(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_price(self, price):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_present_price(self):
        raise NotImplementedError

**Based on Date**

    is_signalInterpreterClass = True
    signal_per_date = []

    @abstractmethod
    def set_data(self, data):
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_date(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_date(self, date: datetime.datetime):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_tomorrow(self):
        raise NotImplementedError

**Based on DateAndPriceLevelBased**

    is_signalInterpreterClass = True
    signal_per_date = []
    signal_per_price = []

    @abstractmethod
    def set_data(self, data):
        raise NotImplementedError

    @abstractmethod
    def interpret_signals(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_date(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_per_price(self):
        raise NotImplementedError

    @abstractmethod
    def get_signal_for_tomorrow(self):
        raise NotImplementedError

### Usage
Used to transform data based on Indicator or DataProcessing and current date or price of stock/other instrument (or combination) 
to simple form: 

    "overpriced": False,
    "underpriced": False,
    "undetermined": True,
    "strength": "strong"

Each Signal is classified by its reliability as strength which may be "strong" or "weak"

## Strategy
### Class Structure
### Usage
Used to based on provided signals make a simple decision: buy, sell or wait. Needs to specify 
minimal strength of provided signals that can be used in decision-making process.yh
