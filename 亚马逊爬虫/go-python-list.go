package main

import (
	"fmt"
	"runtime"

	"github.com/sbinet/go-python"
)

func init() {
	err := python.Initialize()
	if err != nil {
		panic(err.Error())
	}
}

func main() {
	m := python.PyImport_ImportModule("sys")
	pathList := m.GetAttrString("path")

	currentDir := python.PyString_FromString("")
	python.PyList_Insert(pathList, 0, currentDir)

	drawingDiy := python.PyImport_ImportModuleEx("drawingDiy", pathList, pathList, pathList)
	if drawingDiy == nil {
		fmt.Println("Get drawing_diy error!!!")
	}

	spider := drawingDiy.GetAttrString("Spider")
	if spider == nil {
		fmt.Println("Get spider error!!!")
	}
	spi := spider.CallFunction()
	url := spi.GetAttrString("url")
	controler := spi.GetAttrString("controler")
	if controler == nil {
		fmt.Println("Get controler error!!")
	} else {
		controler.CallFunction(python.PyString_AsString(url))
	}

	fetchItemReview := spi.GetAttrString("fetch_single_item_review")
	if fetchItemReview == nil {
		fmt.Println("Get fetch_single_item_review error!!!")
	}
	items := spi.GetAttrString("items")
	item := make(chan *python.PyObject, 3)
	flag := make(chan int)
	go genChan(items, item)
	go fetchItem(fetchItemReview, item, flag)
	<-flag
}

func genChan(items *python.PyObject, item chan *python.PyObject) {
	defer close(item)
	itemSize := python.PyList_GET_SIZE(items)
	for i := 0; i < itemSize; i++ {
		itemURL := python.PyList_GET_ITEM(items, i)
		item <- itemURL
	}
}

func fetchItem(fn *python.PyObject, item chan *python.PyObject, flag chan int) {
	for {
		fmt.Println(runtime.NumGoroutine())
		if url, ok := <-item; ok {
			fn.CallFunction(python.PyString_AsString(url))
		} else {
			break
		}
	}
	flag <- 1
}
