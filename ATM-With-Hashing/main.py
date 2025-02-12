from atm_model import ATM


def main(data_path="customers.json"):
    try:
        atm = ATM(data_path)
        atm.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
