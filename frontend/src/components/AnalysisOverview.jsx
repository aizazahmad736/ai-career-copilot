import React from 'react';
import { Mail, Globe, ExternalLink, MapPin, Briefcase, GraduationCap, FolderGit2 } from 'lucide-react';

export default function AnalysisOverview({ parsedResume, headline, summary }) {
  const info = parsedResume?.personal_info || {};
  const experience = parsedResume?.experience || [];
  const education = parsedResume?.education || [];
  const projects = parsedResume?.projects || [];

  return (
    <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-6 shadow-xl space-y-6">
      {/* Header Profile */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/80">
        <div>
          <div className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-base shadow-md">
              {info.name ? info.name.charAt(0) : 'C'}
            </div>
            <div>
              <h2 className="text-xl font-bold text-white tracking-tight">{info.name || 'Candidate Profile'}</h2>
              <p className="text-xs text-indigo-400 font-medium">{headline || 'Software Engineering Candidate'}</p>
            </div>
          </div>
        </div>

        {/* Links / Contact info */}
        <div className="flex flex-wrap gap-2 text-xs">
          {info.email && (
            <a
              href={`mailto:${info.email}`}
              className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:text-white"
            >
              <Mail className="w-3.5 h-3.5 text-slate-400" />
              <span>{info.email}</span>
            </a>
          )}
          {info.github && (
            <a
              href={info.github.startsWith('http') ? info.github : `https://${info.github}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:text-white"
            >
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <span>GitHub</span>
              <ExternalLink className="w-3 h-3 text-slate-500" />
            </a>
          )}
          {info.linkedin && (
            <a
              href={info.linkedin.startsWith('http') ? info.linkedin : `https://${info.linkedin}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:text-white"
            >
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <span>LinkedIn</span>
              <ExternalLink className="w-3 h-3 text-slate-500" />
            </a>
          )}
          {info.location && (
            <div className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{info.location}</span>
            </div>
          )}
        </div>
      </div>

      {/* Executive Summary */}
      {summary && (
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
            Executive Summary
          </h4>
          <p className="text-sm text-slate-300 leading-relaxed">{summary}</p>
        </div>
      )}

      {/* Experience & Projects Snippet Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Experience */}
        {experience.length > 0 && (
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
              <Briefcase className="w-3.5 h-3.5 text-indigo-400" />
              <span>Experience Highlights</span>
            </h4>
            <div className="space-y-2">
              {experience.slice(0, 2).map((exp, i) => (
                <div key={i} className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
                  <div className="flex justify-between items-start">
                    <p className="text-xs font-semibold text-white">{exp.role}</p>
                    <span className="text-[11px] text-slate-400">{exp.duration}</span>
                  </div>
                  <p className="text-[11px] text-indigo-400">{exp.company}</p>
                  {exp.bullet_points && exp.bullet_points.length > 0 && (
                    <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                      • {exp.bullet_points[0]}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Projects / Education */}
        <div className="space-y-3">
          {projects.length > 0 ? (
            <>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
                <FolderGit2 className="w-3.5 h-3.5 text-indigo-400" />
                <span>Featured Projects</span>
              </h4>
              <div className="space-y-2">
                {projects.slice(0, 2).map((proj, i) => (
                  <div key={i} className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
                    <p className="text-xs font-semibold text-white">{proj.name}</p>
                    <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{proj.description}</p>
                    {proj.tech_stack && proj.tech_stack.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {proj.tech_stack.slice(0, 4).map((tech, t) => (
                          <span key={t} className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                            {tech}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : education.length > 0 ? (
            <>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
                <GraduationCap className="w-3.5 h-3.5 text-indigo-400" />
                <span>Education</span>
              </h4>
              <div className="space-y-2">
                {education.map((edu, i) => (
                  <div key={i} className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
                    <p className="text-xs font-semibold text-white">{edu.degree}</p>
                    <p className="text-xs text-indigo-400">{edu.institution}</p>
                    <p className="text-[11px] text-slate-400 mt-1">Year: {edu.year || 'Recent'}</p>
                  </div>
                ))}
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
