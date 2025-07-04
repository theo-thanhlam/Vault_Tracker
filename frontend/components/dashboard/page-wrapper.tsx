import Link from "next/link"
import { Button } from "../ui/button"
import { ArrowLeft } from "lucide-react"
// import { motion } from "framer-motion"
// import { motion } from "framer-motion"
import * as motion from "motion/react-client"




export default function PageWrapper({ children }: { children: React.ReactNode }) {
    return (

      <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto py-6 space-y-6 w-auto"
    >
 
      <div className="flex gap-4 flex-col items-start">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/dashboard" className="flex items-start gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </Button>
        
      </div>
      {children}
    </motion.div>
  

  )
}