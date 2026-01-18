import React from 'react';
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from 'recharts';

const ConfidenceMeter = ({ score }) => {
    // Score is 0 to 1
    const percentage = Math.round(score * 100);

    const data = [
        {
            name: 'Confidence',
            value: percentage,
            fill: '#00f0ff',
        },
    ];

    return (
        <div className="flex flex-col items-center justify-center p-2">
            <div className="relative w-24 h-24">
                <ResponsiveContainer width="100%" height="100%">
                    <RadialBarChart
                        cx="50%"
                        cy="50%"
                        innerRadius="60%"
                        outerRadius="80%"
                        barSize={10}
                        data={data}
                        startAngle={90}
                        endAngle={-270}
                    >
                        <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                        <RadialBar
                            background={{ fill: '#333' }}
                            clockWise
                            dataKey="value"
                            cornerRadius={10}
                        />
                    </RadialBarChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center text-cyber-neon drop-shadow-[0_0_5px_rgba(0,240,255,0.5)]">
                    <span className="text-xl font-bold">{percentage}%</span>
                    <span className="text-[0.6rem] uppercase text-gray-400">Match</span>
                </div>
            </div>
        </div>
    );
};

export default ConfidenceMeter;
