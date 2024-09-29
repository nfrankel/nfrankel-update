from datetime import datetime

from jinja2 import Environment, FileSystemLoader, Template

from fetch import bio, talks, posts, video


def main() -> None:
    environment = Environment(loader=FileSystemLoader('templates/'))
    template: Template = environment.get_template('template.adoc')
    document: str = template.render(bio=bio(), talks=talks(), posts=posts(), video=video(), updated=datetime.today())
    with open('./nfrankel/README.adoc', 'w') as readme:
        readme.write(document)


if __name__ == '__main__':
    main()
