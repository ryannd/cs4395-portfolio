import Link from 'next/link'
import { useState } from 'react'
import {AiFillCloseSquare,AiFillMinusSquare,AiFillSwitcher} from 'react-icons/ai'

const Assignment = ({title, desc, link, overview}) => {
    const [showOverview, setOverview] = useState(false)
    return (
        <div className="container mx-auto bg-[#C3C3C3] rounded-xl border-4 border-black mt-8">
            <div className="flex w-full m-0 p-2 h-12 bg-[#01007F] border-b-4 border-black rounded-t-lg text-3xl">
                <AiFillCloseSquare style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}}/>
                <AiFillMinusSquare style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}} />
                <AiFillSwitcher style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}}/>
            </div>
            <div className="p-8">
                <h1 className='text-5xl mb-4'>{title}</h1>
                <p className='mb-4'>{desc}</p>
                {showOverview && <div className='container bg-white mb-10 p-5 border-2 border-black shadow-sm text-left'>
                    {overview.split('\n').map((line,i) => <p className='text-lg' key={i}>{line}</p>)}
                </div>}
                {link !== '/' ? <Link href={link}>
                    <button className='bg-[#C3C3C3] border-2 border-black shadow-sm shadow-black p-3'><span style={{fontFamily: 'DotGothic16, sans-serif'}}>Link to assignment</span></button>
                </Link> : ''}
                {overview !== "" ? <button className='bg-[#C3C3C3] border-2 border-black shadow-sm shadow-black p-3 ml-2' onClick={() => setOverview(!showOverview)}><span style={{fontFamily: 'DotGothic16, sans-serif'}}>Show Overview</span></button>: ""}
            </div>
        </div>
    )
}

export default Assignment