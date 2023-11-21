from setuptools import setup

package_name = 'opencv'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ji',
    maintainer_email='ji@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'grayscale      = opencv.grayscale:main',
            'recog_plate    = opencv.recog_plate:main', #final
            'recog_plate1   = opencv.recog_plate1:main',
            'scan           = opencv.scan:main',        #origin
            'scan1           = opencv.scan1:main',      #finial
            'pub_scan       = opencv.pub_scan:main',
        ],
    },
)
