import os
from DataProcessorSingle import DataProcessorSingle

def main():
    print('hi')

if __name__ == "__main__":
    t = DataProcessorSingle('./Example_TEST')
    # main()
    t.process_for_label_images()