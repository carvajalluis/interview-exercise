# Axelar Coding exercise

## Getting up and running

1. install node for serverless framework (brew, nvm, 18.10 ?)
2. install python 3.10 (brew asdf?)
3. install yarn 
4. `yarn install`
5. npx serverless configure
6. have your environment variable file setup to connect to  a test mongo instance 
7. seed your database:
    `python seed.py`
8. deploy your step functions:
    `yarn start`
9. trigger execution on AWS lambda console

## execute lambdas locally :

`python batcher.py`
`python verifier.py`

### **Challenge**

Implement a record signing service using a message driven / micro service solution.

Given a database of 100,000 records and a collection of 100 private keys, create a process to concurrently sign batches of records, storing the signatures in the database until all records are signed.

_Rules_

- No double signing: Only a signature per record should be stored (sign each record individually in batches of X size)
- Any given key in the keyring must not be used concurrently
- A single key should be used for signing all records in a single batch
- Keys should be selected from least recently used to most recently
- Batch size should be configurable by the user (does not change during runtime)

_Guidelines_

- Use a runtime environment of your choosing (we predominantly use Golang and Typescript but language knowledge assessment is not the aim of this challenge)
- Use any orchestration or process coordination tools you see fit (message queues, lambdas, etc)
- Seed the records with any random data
- Use a public key crypto algorithm of your choosing

When you are ready with the challenge, please let us know so we can schedule the next call. 

Feel free to send us any questions on it and/or make any assumption you need along the way while thinking through this.

### Research Best Practices : 
* be compliant with eIDAS
* ECDSA is one of the algorithms specified in eIDAS as an approved cryptographic algorithm for creating advanced electronic signatures (AdES) with legal validity.
