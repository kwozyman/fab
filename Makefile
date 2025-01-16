SHELL := bash
binary=fab

default: build

build: main.go
	go build -o $(binary)
