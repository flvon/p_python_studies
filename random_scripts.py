
test = {
	"test\n": "this is a test"
}

ind = "test\n"



try:
	v = test[ind]
	print(v)
except Exception as err:
	print('error occured')
	print(f'error was: {type(err).__name__} - {err}')

print('the code did not break')