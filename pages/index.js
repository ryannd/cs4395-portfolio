import Head from "next/head"
import Marquee from "react-fast-marquee"
import Assignment from "../components/assignment"
import data from '../data.json'

function HomePage() {
    const assignments = data.assignments.map((obj,idx) => <Assignment title={obj.title} desc={obj.desc} link={obj.link} overview={obj.overview} key={idx}/>)

    return (
        <>
            <Head>
                <title>CS 4395 | Ryan Dimaranan</title>
                <meta property="og:title" content="My page title" key="title" />
            </Head>
            <div className='text-center container mx-auto flex justify-center flex-col mt-5 mb-8'>
                <div className="h-full">
                    <Marquee gradient={false} speed={200}>
                        <h1 className='text-4xl overflow-hidden mr-4'>CS 4395: - Human Language Technologies | Ryan Dimaranan | rtd180003 |</h1>
                    </Marquee>
                </div>
                {assignments.length > 0 ? assignments : <Assignment title="No content" link="/"/>}
            </div>
        </>
        
    )
  }
  
  export default HomePage
  