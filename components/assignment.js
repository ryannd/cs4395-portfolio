import Link from 'next/link'
import {AiFillCloseSquare,AiFillMinusSquare,AiFillSwitcher} from 'react-icons/ai'

const Assignment = ({title, desc, link}) => {
    return (
        <div className="container mx-auto bg-gray-200 rounded-xl border-4 border-black m-10">
            <div className="flex w-full m-0 p-2 h-12 bg-[#D08C60] border-b-4 border-black rounded-t-lg text-3xl">
                <AiFillCloseSquare/>
                <AiFillMinusSquare/>
                <AiFillSwitcher/>
            </div>
            <div className="p-8">
                <h1 className='text-5xl mb-4'>{title}</h1>
                <p className='mb-4'>{desc}</p>
                <div className='rounded bg-gray'>
                    {link !== '/' ? <Link href={link}>
                        <a><p style={{fontFamily: 'DotGothic16, sans-serif'}} className='text-[#997B66]'>Link to assignment</p></a>
                    </Link> : ''}
                </div>
            </div>
        </div>
    )
}

export default Assignment