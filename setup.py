from setuptools import find_packages, setup

package_name = 'yahboom_arm'

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
    maintainer='eduard',
    maintainer_email='codres_ali@yahoo.com',
    description='yahboom robotic arm move joints',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'arm_joint_move = puzzlebot_arm.arm_joint_move:main'
        ],
    },
)
