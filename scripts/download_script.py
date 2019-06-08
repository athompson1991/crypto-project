from core.downloader import Downloader
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true")
    args = parser.parse_args()

    project_dir = "/Users/alex/ml_class/project/"

    print("Configuring")
    if args.prod:
        downloader = Downloader(False)
    else:
        downloader = Downloader(True)
    downloader.configure(project_dir + "scripts/config.json")
    downloader.make_client()
    print("Fetching data")
    downloader.fetch()
    print("Saving to csv files")
    downloader.to_csv(project_dir, 'data')
