import cx_Freeze

executables = [cx_Freeze.Executable('fazaa.py')]

cx_Freeze.setup(
	name = 'Fazaa',
	options = {'build_exe':{'packages':['pygame'], "include_files":['background.png', 'background2.png', 'bigbrown1.png',
	'bigbrown2.png', 'bigbrown3.png', 'bigbrown4.png', 'biggrey1.png', 'biggrey2.png', 'biggrey3.png', 'biggrey4.png',
	'booms.ogg', 'Deus_Ex_Tempus.mp3', 'explosion.ogg', 'explosion2.ogg', 'gunPower.png', 'kenvector_future.ttf',
	'laser.wav', 'medbrown1.png', 'medbrown2.png', 'medgrey1.png', 'medgrey2.png', 'redLaser.png', 'redLife.png',
	'redPlayer.png', 'regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png', 'regularExplosion03.png',
	'regularExplosion04.png', 'regularExplosion05.png', 'regularExplosion06.png', 'regularExplosion07.png',
	'regularExplosion08.png', 'shield.png', 'shieldPower.png', 'smallbrown1.png', 'smallbrown2.png', 'smallgrey1.png',
	'smallgrey2.png', 'sonicExplosion00.png', 'sonicExplosion01.png', 'sonicExplosion02.png', 'sonicExplosion03.png',
	'sonicExplosion04.png', 'sonicExplosion05.png', 'sonicExplosion06.png', 'sonicExplosion07.png', 'sonicExplosion08.png',
	'thrust.png', 'tinybrown1.png', 'tinybrown2.png', 'tinygrey1.png', 'tinygrey2.png']}},
	executables = executables
	)