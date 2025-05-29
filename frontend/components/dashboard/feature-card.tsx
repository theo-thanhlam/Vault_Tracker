import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'
import { FolderTree, Receipt } from 'lucide-react'
import { Button } from '@/components/ui/button'


interface FeatureCardProps {
  title: string
  description: string
  icon: React.ReactNode
  href: string
}

const FeatureCard = ({ title, description, icon, href }: FeatureCardProps) => {
  return (
    <Link href={href}>
          <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {icon}
                {title}
              </CardTitle>
              <CardDescription>
                {description}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" className="w-full border border-primary">
                View {title}
              </Button>
            </CardContent>
          </Card>
        </Link>
  )
}

export default FeatureCard