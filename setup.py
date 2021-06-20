import pathlib
from setuptools import setup, find_packages

UPSTREAM_URLLIB3_FLAG = '--with-upstream-urllib3'

def get_requirements(raw=False):
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as reqs:
        for install in reqs:
            if install.startswith('# only telegram.ext:'):
                if raw:
                    break
                continue
            requirements_list.append(install.strip())

    return requirements_list


def get_packages_requirements(raw=False):
    """Build the package & requirements list for this project"""
    reqs = get_requirements(raw=raw)

    exclude = ['tests*']
    if raw:
        exclude.append('telegram.ext*')

    packs = find_packages(exclude=exclude)
    # Allow for a package install to not use the vendored urllib3
    if UPSTREAM_URLLIB3_FLAG in sys.argv:
        sys.argv.remove(UPSTREAM_URLLIB3_FLAG)
        reqs.append('urllib3 >= 1.19.1')
        packs = [x for x in packs if not x.startswith('telegram.vendor.ptb_urllib3')]

    return packs, reqs

packages, requirements = get_packages_requirements()

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(name="sentimentalmarket",
      version="0.0.1",
      description="Its a library which helps to do crypto trading in binance",
      long_description=README,
      long_description_content_type="text/markdown",
      include_package_data=True,
      setup_requires=['wheel'],
      packages=packages,
      install_requires=requirements,
      author='Sabu George',
      author_email='sabugeorge.mec@gmail.com',
      license='Apache-2.0 License',
      python_requires='>=3.6',
      )
