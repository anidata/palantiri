from distutils.core import setup

setup(
        name="palantiri",
        version="0.0.1",
        description="Crawler to find data on adds involving human trafficking",
        author="Daniel Robertson",
        author_email="danlrobertson89@gmail.com",
        license="MPL 2.0",
        packages=["palantiri", "palantiri.core"],
        package_dir={'palantiri': 'src'}
        )
