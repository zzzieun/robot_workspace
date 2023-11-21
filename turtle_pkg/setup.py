from setuptools import setup
import math

package_name = 'turtle_pkg'

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
            #'square = turtle_pkg.move_turtle:main',
            'circle = turtle_pkg.move_turtle:main',
            'sub_pose = turtle_pkg.sub_pose:main',
            'remote_turtle= turtle_pkg.remote_turtle:main',
            'rotate_turtle= turtle_pkg.rotate_turtle:main',
            'rotate_turtle2= turtle_pkg.rotate_turtle2:main',
            'rotate_turtle3= turtle_pkg.rotate_turtle3:main',

        ],
    },
)
