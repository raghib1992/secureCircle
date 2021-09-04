# pip install dryable


import dryable

# @dryable.Dryable( label = 'labelA' )
# def functionA():
#     print( "Hi, I am A" )

# @dryable.Dryable( label = 'labelB' )
# def functionB():
#     print( "Hi, I am B" )

# dryable.set( True, 'labelB' )
# functionA() # this will be dried up
# functionB() # this will run for real


@dryable.Dryable()
def print_name(name):
    print("My name is {}".format(name))
# if false then function will run
dryable.set(True)
print_name('Raghib')