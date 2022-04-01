
import React from 'react'
import {useRouter} from 'next/router'

export default function inedx() {
    const router = useRouter()
    const id = router.query?.id ?? "Unknown"
    return (
        <div>
        foo page  {id}

             
        </div>
    )
}

