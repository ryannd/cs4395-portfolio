import Link from 'next/link'
import { useState } from 'react'
import {AiFillCloseSquare,AiFillMinusSquare,AiFillSwitcher} from 'react-icons/ai'

const Assignment = ({title, desc, link, overview}) => {
    const [showOverview, setOverview] = useState(false)
    const [minimize, setMinimize] = useState(false)

    const doMinimize = () => {
        if(minimize) {
            document.getElementById(`content-${title}`).classList.remove('hidden')
            setMinimize(false)
        } else {
            document.getElementById(`content-${title}`).classList.add('hidden')
            setMinimize(true)
        }
    }
    return (
        <div className="container mx-auto bg-[#C3C3C3] sm:rounded-xs md:rounded-md xl:rounded-xl border-4 border-black mt-8">
            <div className="flex justify-between w-full h-full m-0 p-2 h-12 bg-gradient-to-r from-[#01007F] to-[#A4C9EF] border-b-4 border-black xs:rounded-xs md:rounded-sm xl:rounded-t-lg">
                <div className='h-full items-center justify-center'>
                    <h1 style={{marginLeft: '10px'}} className='text-white 2xl:text-xl md:text-md'>{title}</h1>
                </div>
                <div className='flex 2xl:text-3xl md:text-xl'>
                    <AiFillCloseSquare style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}}/>
                    <AiFillSwitcher style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}}/>
                    <AiFillMinusSquare style={{color: '#C3C3C3', backgroundColor: 'black', marginRight: '10px'}} onClick={() => doMinimize()}/>
                </div>
            </div>
            <div className="p-8" id={`content-${title}`}>
                <h1 className='2xl:text-4xl md:text-2xl mb-4'>{title}</h1>
                <p className='mb-4'>{desc}</p>
                {showOverview && <div className='container bg-white mb-10 p-5 border-2 border-black shadow-sm text-left'>
                    {overview.split('\n').map((line,i) => <p className='2xl:text-lg' key={i}>{line}</p>)}
                </div>}
                {link !== '/' ? <Link href={link}>
                    <button className='bg-[#C3C3C3] border-2 border-black shadow-sm shadow-black p-3'><span style={{fontFamily: 'DotGothic16, sans-serif'}}>Link to assignment</span></button>
                </Link> : ''}
                {overview !== "" ? <button className='bg-[#C3C3C3] border-2 border-black shadow-sm shadow-black p-3 ml-2' onClick={() => setOverview(!showOverview)}><span style={{fontFamily: 'DotGothic16, sans-serif'}}>{showOverview ? "Hide Overview" : "Show Overview"}</span></button>: ""}
            </div>
        </div>
    )
}

export default Assignment