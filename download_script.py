from downloader import Downloader
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true")
    args = parser.parse_args()

    print("Configuring")
    if args.prod:
        downloader = Downloader(False)
    else:
        downloader = Downloader(True)
    downloader.configure()
    downloader.make_client()
    print("Fetching data")
    downloader.fetch()
    print("Saving to csv files")
    downloader.to_csv('data')
