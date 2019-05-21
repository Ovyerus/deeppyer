import setuptools

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as req:
    packages = req.read().splitlines()

setuptools.setup(
    name='deeppyer',
    version='1.0.1',
    author='Ovyerus',
    author_email='iamovyerus@gmail.com',
    description='Deepfry images in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Ovyerus/deeppyer',

    packages=setuptools.find_packages(),
    install_requires=packages,
    include_package_data=True,

    entry_points={
        'console_scripts': ['deeppyer=deeppyer.cli:main']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Multimedia :: Graphics',
        'Typing :: Typed'
    ],
    python_requires='>=3.6',
    keywords='image manipulation deepfry meme'
)
