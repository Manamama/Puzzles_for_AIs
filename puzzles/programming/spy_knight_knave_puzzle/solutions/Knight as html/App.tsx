
import React, { useMemo } from 'react';
import { Role, Person, RolesMap, VerificationResult } from './types';

// Helper to generate all permutations of an array
function* permutations<T>(arr: T[], size: number = arr.length): Generator<T[]> {
  if (size > arr.length) return;
  const indices = Array.from({ length: arr.length }, (_, i) => i);
  const cycles = Array.from({ length: size }, (_, i) => arr.length - i);

  yield arr.slice(0, size).map(i => i);

  while (true) {
    let i = size - 1;
    while (i >= 0) {
      cycles[i]--;
      if (cycles[i] === 0) {
        const temp = indices[i];
        for (let j = i; j < arr.length - 1; j++) {
          indices[j] = indices[j + 1];
        }
        indices[arr.length - 1] = temp;
        cycles[i] = arr.length - i;
      } else {
        const j = cycles[i];
        [indices[i], indices[arr.length - j]] = [indices[arr.length - j], indices[i]];
        yield indices.slice(0, size).map(k => arr[k]);
        break;
      }
      i--;
    }
    if (i < 0) return;
  }
}

const App: React.FC = () => {

    const verificationResults = useMemo(() => {
        const roles: Role[] = ['knight', 'knave', 'spy'];
        const people: Person[] = ['A', 'B', 'C'];
        
        const statements: Record<Person, (roles: RolesMap) => boolean> = {
            A: (r) => r['C'] === 'knave',
            B: (r) => r['A'] === 'knight',
            C: (r) => r['C'] === 'spy',
        };

        const results: VerificationResult[] = [];
        let id = 1;

        for (const perm of permutations(roles)) {
            const assignedRoles = {
                A: perm[0],
                B: perm[1],
                C: perm[2],
            } as RolesMap;
            
            const log: VerificationResult['log'] = [];
            let isPermutationConsistent = true;

            for (const person of people) {
                const personRole = assignedRoles[person];
                const statementIsTrue = statements[person](assignedRoles);
                let isStepConsistent = true;
                let message = '';

                if (personRole === 'knight') {
                    if (!statementIsTrue) {
                        message = `Inconsistent: Knight ${person} made a false statement.`;
                        isStepConsistent = false;
                        isPermutationConsistent = false;
                    } else {
                        message = `Consistent: Knight ${person} made a true statement.`;
                    }
                } else if (personRole === 'knave') {
                    if (statementIsTrue) {
                        message = `Inconsistent: Knave ${person} made a true statement.`;
                        isStepConsistent = false;
                        isPermutationConsistent = false;
                    } else {
                         message = `Consistent: Knave ${person} made a false statement.`;
                    }
                } else if (personRole === 'spy') {
                    message = `Neutral: Spy ${person}'s statement can be true or false.`;
                }
                
                log.push({ message, isConsistent: isStepConsistent });
                if (!isPermutationConsistent) break;
            }
            results.push({ id: id++, permutation: assignedRoles, log, isSolution: isPermutationConsistent });
        }
        return results;
    }, []);

    return (
        <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-4 sm:p-6 md:p-8">
            <div className="w-full max-w-6xl mx-auto">
                <header className="text-center mb-10">
                    <h1 className="text-4xl md:text-5xl font-bold text-amber-300 tracking-tight">The Puzzle of the Knight, Knave, and Spy</h1>
                    <p className="text-slate-400 mt-2 text-lg">A Step-by-Step Logical Deduction</p>
                </header>

                <main className="space-y-12">
                    {/* The Premise & Statements */}
                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
                             <h2 className="text-2xl font-semibold text-rose-400 mb-4">The Premise</h2>
                             <ul className="space-y-3 text-slate-300">
                                <li><span className="font-bold text-white">The Knight:</span> Always tells the truth.</li>
                                <li><span className="font-bold text-white">The Knave:</span> Always lies.</li>
                                <li><span className="font-bold text-white">The Spy:</span> Can either lie or tell the truth.</li>
                             </ul>
                        </div>
                         <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
                             <h2 className="text-2xl font-semibold text-amber-400 mb-4">The Statements</h2>
                             <ul className="space-y-3 text-slate-300">
                                <li><span className="font-bold text-white">A says:</span> "C is a knave."</li>
                                <li><span className="font-bold text-white">B says:</span> "A is a knight."</li>
                                <li><span className="font-bold text-white">C says:</span> "I am the spy."</li>
                             </ul>
                        </div>
                    </div>

                    {/* The Deduction */}
                    <div className="bg-slate-800/70 p-6 md:p-8 rounded-xl border border-slate-700">
                        <h2 className="text-3xl font-bold text-teal-300 mb-6 text-center">The Logical Deduction</h2>
                        <div className="space-y-6 text-slate-300 leading-relaxed">
                            <p><strong className="text-white">Step 1: Analyze C's statement.</strong> C says, "I am the spy."</p>
                            <ul className="list-disc list-inside pl-4 space-y-2">
                                <li>If C were the <span className="font-semibold text-rose-300">Knight</span>, he would have to tell the truth. But then he would be the Spy, not the Knight. This is a contradiction.</li>
                                <li>Therefore, <strong className="text-white">C cannot be the Knight.</strong></li>
                            </ul>
                            
                            <p><strong className="text-white">Step 2: Consider the remaining possibilities for the Knight.</strong> Since C is not the Knight, the Knight must be either A or B.</p>
                            
                            <p><strong className="text-white">Step 3: Test the hypothesis that B is the Knight.</strong></p>
                             <ul className="list-disc list-inside pl-4 space-y-2">
                                <li>Let's assume B is the <span className="font-semibold text-rose-300">Knight</span>. His statement, "A is a knight," must be true.</li>
                                <li>This would mean A is also the Knight. However, there can only be one Knight. This is a contradiction.</li>
                                <li>Therefore, our assumption was wrong. <strong className="text-white">B cannot be the Knight.</strong></li>
                             </ul>

                            <p><strong className="text-white">Step 4: Determine the identity of the Knight.</strong></p>
                             <ul className="list-disc list-inside pl-4">
                                <li>We have eliminated C and B as the Knight. By process of elimination, <strong className="text-white">A must be the Knight.</strong></li>
                             </ul>

                            <p><strong className="text-white">Step 5: Deduce the remaining identities and verify.</strong></p>
                            <ul className="list-disc list-inside pl-4 space-y-2">
                                <li>Since A is the Knight, his statement "C is a knave" must be true. So, <strong className="text-white">C is the Knave.</strong></li>
                                <li>This leaves only one role for B: <strong className="text-white">B must be the Spy.</strong></li>
                                <li>Let's verify this solution against the statements:
                                    <ul className="list-circle list-inside pl-6 mt-2 space-y-1">
                                        <li>A (Knight) says "C is a knave." This is true. ✅</li>
                                        <li>B (Spy) says "A is a knight." This is true. A Spy can tell the truth. ✅</li>
                                        <li>C (Knave) says "I am the spy." This is false. A Knave must lie. ✅</li>
                                    </ul>
                                </li>
                                <li className="pt-2">All statements are consistent with this assignment.</li>
                            </ul>
                        </div>
                    </div>

                     {/* The Solution */}
                    <div className="text-center p-6 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-lg">
                        <h2 className="text-2xl font-bold text-white mb-2">The Solution</h2>
                        <div className="text-xl text-slate-900 font-semibold space-x-6">
                            <span>A is the Knight</span>
                            <span>B is the Spy</span>
                            <span>C is the Knave</span>
                        </div>
                    </div>

                    {/* Computational Verification Section */}
                    <div className="bg-slate-800/70 p-6 md:p-8 rounded-xl border border-slate-700">
                        <h2 className="text-3xl font-bold text-sky-300 mb-6 text-center">Computational Verification</h2>
                        <p className="text-center text-slate-400 mb-8">Checking all 6 possible realities to find the single consistent solution.</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {verificationResults.map(result => (
                                <div key={result.id} className={`p-4 rounded-lg border ${result.isSolution ? 'bg-teal-900/50 border-teal-500' : 'bg-slate-800/60 border-slate-700'}`}>
                                    <h3 className="font-bold text-lg text-white mb-3">
                                        #{result.id}: A=<span className="capitalize">{result.permutation.A}</span>, B=<span className="capitalize">{result.permutation.B}</span>, C=<span className="capitalize">{result.permutation.C}</span>
                                    </h3>
                                    <ul className="space-y-2 text-sm">
                                        {result.log.map((logEntry, index) => (
                                            <li key={index} className="flex items-start">
                                                <span className={`mr-2 mt-1 ${logEntry.isConsistent ? 'text-green-400' : 'text-red-400'}`}>
                                                    {logEntry.isConsistent ? '✅' : '❌'}
                                                </span>
                                                <span className="text-slate-300">{logEntry.message}</span>
                                            </li>
                                        ))}
                                    </ul>
                                    {result.isSolution && (
                                         <p className="mt-3 text-center font-bold text-green-300 bg-green-900/50 py-1 rounded">VALID SOLUTION</p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>

                </main>
            </div>
        </div>
    );
};

export default App;
