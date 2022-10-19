# Introduction

The tests folder contains some tests for the pets site: https://petfriends.skillfactory.ru/

All tests were created within the educational project and can be improved.

Link on Swager doc: https://petfriends.skillfactory.ru/apidocs/ 

# How To Run Tests

To run test_get suite execute:

        py.test -v -m 'get'
  
To run test_add tests:

          py.test -v -m 'add'
  
To run test_other tests:

        py.test -v -m 'other'
  
To run negative test suite:
        
        py.test -v -m 'neg'
  
Also you can run test with additional parametres: 
  - auth (all authorization tests)
  - act (all tests action with pets)
  - pos (all positive tests)

Please, run "py.test -v -m 'del_all'", when you finish working with the tests.

# Note

Some tests were skipped, for demonstrating the skip possibility. The project can be improved and supplemented.
