import Link from "next/link"
import { Button } from "../ui/button"
import { ArrowLeft } from "lucide-react"


export default function PageWrapper({ children }: { children: React.ReactNode }) {
    return (
    <div className="container mx-auto py-6 space-y-6 w-auto">
      <div className="flex gap-4 flex-col items-start">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/dashboard" className="flex items-start gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </Button>
        
      </div>
      {children}
    </div>
  )
}