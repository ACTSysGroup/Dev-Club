import React, { useState } from 'react'
import sty from './index.module.scss'

//TODO List:

//1. Add TODO Item ✅
//2. Delete TODO Item ✅
//3. Finish TODO Item
type TItemList = {
    item: string,
    idx: number
    isItemDone: Map<string, boolean>
    onClick: (idx: number) => void
    onFinish: (s: string) => void

}
const ItemList = (props: TItemList) => {
    const isItemDone = props.isItemDone
    const s = props.item
    const idx = props.idx
    // const { onClick, onFinish } = props
    const onClick = props.onClick
    const onFinish = props.onFinish


    return <div className={sty.item}>

        <span>
            State:
            {
                isItemDone.has(s) ?
                    <span className={sty.done}>"已完成"</span> :
                    <span className={sty.unfinished}> "未完成"</span>
            }
        </span>
        <span>
            事项: {s}
        </span>
        <div className={sty.action}>
            <button onClick={() => onClick(idx)}>Delete</button>
            <button onClick={() => onFinish(s)}>Finish</button>
        </div>



    </div>


}
//f(S) = U
export default function Index() {

    const [todoItems, setTodoItems] = useState([
        "item 1",
        "item 2",
        "item 3",
    ])

    const [isItemDone, setTodoState] = useState<Map<string, boolean>>(new Map())


    const onClick = (idx: number) => {
        console.log("deleting ", idx)
        setTodoItems([
            ...todoItems.slice(0, idx),
            ...todoItems.slice(idx + 1, todoItems.length)
        ])


    }


    const onAdd = () => {
        setTodoItems([
            ...todoItems,
            `items ${todoItems.length + 1}`
        ])
    }


    const onFinish = (items: string) => {
        isItemDone.set(items, true)
        const newState: typeof isItemDone = new Map()
        Array
            .from(isItemDone.keys())
            .forEach(k => {
                newState.set(k, isItemDone.get(k))
            })

        setTodoState(newState)
    }
    return (
        <div>
            {
                todoItems.map((s, idx) => (
                    <div key={idx}>
                        <ItemList
                            item={s}
                            idx={idx}
                            onClick={onClick}
                            onFinish={onFinish}
                            isItemDone={isItemDone}
                        />
                    </div>
                ))
            }

            <div>
                <button onClick={onAdd}> Add Item</button>

            </div>
        </div>
    )

}
