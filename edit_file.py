import click

@click.command()
@click.option("--file_path", default="evocraft_ga/external/eula.txt", help="Path to eula.txt")
@click.option('--find_str', default="eula=false", help='string to replace')
@click.option('--replace_str', default="eula=true", help='value for replacement')
def edit_file(file_path, find_str, replace_str="eula=True"):
    with open(file_path, 'r') as f:
        file_str = f.read()

    print("Replacing {} with {}".format(find_str, replace_str))
    file_str = file_str.replace(find_str, replace_str)

    with open(file_path, 'w') as f:
        f.writelines(file_str)

if __name__ == '__main__':
    edit_file()