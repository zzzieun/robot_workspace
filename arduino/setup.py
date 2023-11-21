from setuptools import setup

package_name = 'arduino'

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
             'pub_led_msg   = arduino.script.pub_led_msg:main',
             'sub_led_msg   = arduino.script.sub_led_msg:main',
        ],
    },
)
