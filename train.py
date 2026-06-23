# import sys

# def train_model(dataset_path, learning_rate, batch_size):
#     print(f"Loading data from: {dataset_path}")
#     print(f"Hyperparameters: Learning Rate = {learning_rate}, Batch Size = {batch_size}")
#     print("Training model...")
#     # Your model training logic goes here

# if __name__ == "__main__":
#     # sys.argv[0] is always the script name itself
#     if len(sys.argv) < 4:
#         print("Error: Missing arguments.")
#         print("Usage: python train.py <dataset_path> <learning_rate> <batch_size>")
#         sys.exit(1)

#     # Parsing arguments based on position
#     data_path = sys.argv[1]
#     lr = float(sys.argv[2])
#     batch = int(sys.argv[3])

#     # Execute training
#     train_model(data_path, lr, batch)
## Commands in terminal : python train.py "table.csv" 0.01 126

import argparse

def train_model(dataset_path, learning_rate, batch_size):
    print(f"Selected Dataset: {dataset_path}")
    print(f"Loading data from: {dataset_path}")
    print(f"Hyperparameters: LR = {learning_rate}, Batch = {batch_size}")
    print("Training model...")

if __name__ == "__main__":
    # 1. Create the parser object
    # Also free documentation for the script
    parser = argparse.ArgumentParser(description="Train a Machine Learning Model" \
    " It accepts : --data , --lr and --batch")

    # 2. Define your arguments with names, types, and defaults
    parser.add_argument("--data", type=str, required=True, help="Path to the dataset CSV")
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate (default: 0.01)")
    parser.add_argument("--batch", type=int, default=32, help="Batch size (default: 32)")

    # 3. Parse the arguments
    args = parser.parse_args()

    # 4. Pass the variables to your function
    train_model(args.data, args.lr, args.batch)

## Command in terminal : python train.py --data "table.csv"  --batch 16 --lr 0.01

## We can even loop the inputs via terminal !!!!
'''  
foreach ($lr in 0.1, 0.01, 0.001) {
    python train_argparse.py --data "table.csv" --lr $lr --batch 64
}
'''