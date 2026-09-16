from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ag',
    maintainer_email='ahmedmgaber28@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_node = my_py_pkg.node:main',
            'simple_publisher = my_py_pkg.simple_publisher:main',
            'simple_subscriber = my_py_pkg.simple_subscriber:main',
            'robot_news_station = my_py_pkg.robot_news_station:main',
            'smart_phone = my_py_pkg.smart_phone:main',
            'number_publisher = my_py_pkg.number_publisher:main',
            'number_counter = my_py_pkg.number_counter:main',
        ],
    },
)
