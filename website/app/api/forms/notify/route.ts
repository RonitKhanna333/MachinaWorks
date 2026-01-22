import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { formData, type } = await request.json()

    // Validate input
    if (!formData || !type) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Just log the submission for now (no email, no database)
    console.log(`[${type.toUpperCase()}] Submission from ${formData.email}:`, formData)

    return NextResponse.json(
      { success: true, message: 'Submission received' },
      { status: 200 }
    )
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json(
      { error: 'Failed to process submission' },
      { status: 500 }
    )
  }
}
