from setuptools import setup

package_name = 'tb3_pkg'

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
            'remote_tb3 = tb3_pkg.remote_tb3:main',
            'sub_odom = tb3_pkg.sub_odom:main',
            'sub_odom2 = tb3_pkg.sub_odom2:main',
            'sub_laser = tb3_pkg.sub_laser:main',
        ],
    },
)
